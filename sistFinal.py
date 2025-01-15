import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='rootroot',
    database='bdsistemacampeonatos',
)
cursor = conexao.cursor()

class Campeonato:
    def __init__(self, nome):
        self.__nome = nome
        self.__campeao = None

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novoNome):
        self.__nome = novoNome

    @property
    def campeao(self, cursor):
        query = f'''
        SELECT cl.idclube, cl.nome, cl.pontos
        FROM clube cl JOIN campeonato ca 
        ON cl.idcampeonato = ca.idcampeonato
        ORDER BY cl.pontos DESC
        LIMIT 1;
        '''
        cursor.execute(query, (self.__nome,))
        campeao = cursor.fetchone()
        return campeao
    
    def removerCampeonato(self, cursor, conexao):
        try:
            query = f'''
            delete from campeonato
            where nome = "{self.__nome.lower()}"
            '''
            cursor.execute(query)
            conexao.commit()
            print('Campeonato removido com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

    def adicionarClube(self, nome, cursor, conexao):
        try:
            nome_clube = input('Digite o nome do clube que entrará no campeonato: ')
            query = f'''
            update clube
            set idcampeonato = (select idcampeonato from campeonato where nome = "{self.__nome.lower()}")
            where nome = "{nome_clube.lower()}"
            '''
            cursor.execute(query)
            conexao.commit()
            print(f'{nome_clube} está participando de {self.__nome}!')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

    def removerClube(self, nome, cursor, conexao):
        try:
            nome_clube = input('Digite o nome do clube que sairá do campeonato: ')
            
            query_verificar = f'''
            select cl.idclube
            from clube cl join campeonato ca
            on cl.idcampeonato = ca.idcampeonato
            where ca.nome = "{self.__nome}" and cl.nome = "{nome_clube}"
            '''
            cursor.execute(query_verificar)
            resultado = cursor.fetchone()

            idclube = resultado[0]
            
            query_retirar = f'''
            update clube
            set idcampeonato = null
            where idclube = "{idclube}"
            '''
            
            cursor.execute(query_retirar)
            conexao.commit()
            print(f'{nome_clube} saiu de {self.__nome}!')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

    def exibirTabela(self, cursor):
        try:
            query = f'''
            select cl.idclube, cl.nome, cl.pontos
            from campeonato ca left join clube cl
            on ca.idcampeonato = cl.idcampeonato
            where ca.idcampeonato = (select idcampeonato from campeonato where nome = "{self.__nome.lower()}")
            order by cl.pontos desc
            '''
            cursor.execute(query)
            resultado = cursor.fetchall()
            for row in resultado:
                print(f'Id: {row[0]}, Clube: {row[1]}, Pontuação: {row[2]}')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

class Partida:
    def __init__(self, clube1, clube2):
        self.__clube1 = clube1
        self.__clube2 = clube2
        
    @property
    def campeonato(self):
        return self.__campeonato
    
    @campeonato.setter
    def campeonato(self, campeonato):
        if isinstance(campeonato, Campeonato):
            self.__campeonato = campeonato
        else:
            raise ValueError('O valor fornecido não é uma instância válida de Partida.')

    @property
    def clube1(self):
        return self.__clube1
    
    @clube1.setter
    def clube1(self, clube1):
        if isinstance(clube1, Clube):
            self.__clube1 = clube1
        else:
            raise ValueError('O valor fornecido não é uma instãncia válida de Clube')

    @property
    def clube2(self):
        return self.__clube2
    
    @clube2.setter
    def clube2(self, clube2):
        if isinstance(clube2, Clube):
            self.__clube2 = clube2
        else:
            raise ValueError('O valor fornecido não é uma instãncia válida de Clube')
    
class Clube:
    def __init__(self, nome, jogos, gols, pontos):
        self.__nome = nome
        self.__jogos = jogos
        self.__gols = gols
        self.__pontos = pontos

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, novoNome):
        self.__nome = novoNome

    @property
    def jogos(self):
        return self.__jogos

    @jogos.setter
    def jogos(self, novoJogos):
        self.__jogos = novoJogos

    @property
    def gols(self):
        return self.__gols
    
    @gols.setter
    def gols(self, novoGols):
        self.__gols = novoGols

    @property
    def pontos(self):
        return self.__pontos

    @pontos.setter
    def pontos(self, novoPonto):
        self.__pontos = novoPonto 

    def removerClube(self, nome, cursor, conexao):
        try:
            query = f'''
            delete from clube
            where nome = "{nome.lower()}"
            '''
            cursor.execute(query)
            conexao.commit()
            print('Clube removido com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

    def consultaClube(self, nome, cursor):
        try:
            query = f'''
            select c.idclube, c.nome, c.jogos, c.saldoGols, c.pontos, j.nome, j.sobrenome
            from clube c left join jogador j
            on c.idclube = j.idclube
            where c.nome = "{nome.lower()}";
            '''
            cursor.execute(query)
            resultado = cursor.fetchall()
            print(f'Clube: {resultado[0][1]}, Jogos: {resultado[0][2]}, Gols feitos: {resultado[0][3]}, Pontos: {resultado[0][4]}')
            print('Jogadores:')
            for row in resultado:  
                print(f'- {row[5]} {row[6]}')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")    

class Jogador:
    def __init__(self, nome, sobrenome, dt_nascimento):
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__dt_nascimento = dt_nascimento
        self.__jogos = 0
        self.__gols = 0
        self.__assistencias = 0

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, novoNome):
        self.__nome = novoNome

    @property
    def sobrenome(self):
        return self.__sobrenome
    
    @sobrenome.setter
    def sobrenome(self, novoSobrenome):
        self.__sobrenome = novoSobrenome

    @property
    def dt_nascimento(self):
        return self.__dt_nascimento
    
    @dt_nascimento.setter
    def dt_nascimento(self, novadt_nascimento):
        self.__dt_nascimento = novadt_nascimento
     
    @property
    def jogos(self):
        return self.__jogos

    @jogos.setter
    def jogos(self, novoJogos):
        self.__jogos = novoJogos

    @property
    def gols(self):
        return self.__gols

    @gols.setter
    def gols(self, novoGols):
        self.__gols = novoGols

    @property
    def assistencias(self):
        return self.__assistencias
    
    @assistencias.setter
    def assistencias(self, novoAssistencias):
        self.__assistencias = novoAssistencias
    
    def removerJogador(self, cursor, conexao):
        try:
            query = f'''
            delete from jogador
            where sobrenome = "{self.__sobrenome.lower()}"
            '''
            cursor.execute(query)
            conexao.commit()
            print('Atleta removido com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

    def mudarClube(self, sobrenome_jogador, cursor, conexao):
        try:
            nome_clube = input('Digite o nome do clube novo: ')
            query = f'''
            update jogador
            set idclube = (SELECT idclube FROM clube WHERE nome = "{nome_clube.lower()}") 
            where sobrenome = "{sobrenome_jogador.lower()}"
            '''
            cursor.execute(query)
            conexao.commit()
            print(f'Agora {self.__nome} {sobrenome_jogador} é do(a) {nome_clube}')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

    def demitirJogador(self, sobrenome_jogador, cursor, conexao):
        try:
            nome_clube = input('Digite o nome do clube: ')

            query_verificar = f'''
            select j.idjogador
            from jogador j join clube c
            on j.idclube = c.idclube
            where c.nome = "{nome_clube.lower()}" and j.sobrenome = "{sobrenome_jogador.lower()}"
                '''
            cursor.execute(query_verificar)
            resultado = cursor.fetchone()

            idjogador = resultado[0]

            query_demitir = f'''
            update jogador
            set idclube = null 
            where idjogador = {idjogador}
            '''
            cursor.execute(query_demitir)
            conexao.commit()
            print(f'Jogador {self.__nome} {sobrenome_jogador} foi demitido do clube {nome_clube}.')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

    def consultaAtleta(self, cursor):
        try:
            query = f'''
            select j.nome, j.sobrenome, c.nome, j.dt_nascimento, j.jogos, j.gols, j.assistencias
            from jogador j left join clube c
            on j.idclube = c.idclube
            where j.sobrenome = "{self.__sobrenome}"
            '''
            cursor.execute(query)
            resultado = cursor.fetchone()
            print(f'Nome: {resultado[0]}, Sobrenome: {resultado[1]}, Clube: {resultado[2]}, Data de Nascimento: {resultado[3]}\nJogos: {resultado[4]}, Gols: {resultado[5]}, Assistências: {resultado[6]}')
        except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

def inscreverCampeonato(cursor, conexao):
    try:
        nome = input('Digite o nome do Campeonato: ')
        query = f'''
        insert into campeonato (nome)
        values ("{nome}")
        '''
        cursor.execute(query)
        conexao.commit()
        print(f'Campeonato {nome.lower()} criado com sucesso!')
    except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

def inscreverClube(cursor, conexao):
    try:
        nome = input('Digite o nome do clube: ')
        query = f'''
        insert into clube (nome, jogos, saldoGols, pontos)
        values ("{nome.lower()}", 0, 0, 0)
        '''
        cursor.execute(query)
        conexao.commit()
        print('Clube registrado com sucesso!')
    except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

def inscreverAtleta(cursor, conexao):
    try:
        nome = input('Digite o nome do Atleta: ')
        sobrenome = input('Digite o sobrenome do Atleta: ')
        dt_nascimento = input('Digite a data de nascimento do jogador (aaaa/mm/dd): ')
        query = f'''
        insert into jogador (nome, sobrenome, dt_nascimento, gols, assistencias, jogos)
        values ("{nome.lower()}", "{sobrenome.lower()}", "{dt_nascimento.lower()}", 0, 0, 0)
        '''
        cursor.execute(query)
        conexao.commit()
        print('Jogador registrado com sucesso!')
    except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

def marcarGol(idpartida, cursor, conexao):
    try:
        clube = input('Qual equipe fez o gol (1 ou 2): ')

        if clube == '1':
            query = f'update partida set placarclube1 = placarclube1 + 1 where idpartida = {idpartida};'
            cursor.execute(query)
            conexao.commit()

        elif clube =='2':
            query = f'update partida set placarclube2 = placarclube2 + 1 where idpartida = {idpartida};'
            cursor.execute(query)
            conexao.commit()

        else:
            raise ValueError('Opcção inválida digite 1 ou 2')
        clube = (input('Confirme o clube:'))
        query = f'update clube set saldoGols = saldoGols + 1 where nome = "{clube}"'
        cursor.execute(query)
        conexao.commit()
        sobrenome_artilheiro = input('Digite o sobrenome do jogador que fez o gol: ')
        
        query = f'update jogador set gols = gols + 1 where sobrenome = "{sobrenome_artilheiro}"'
        cursor.execute(query)
        conexao.commit()
        
        sobrenome_assistente = input('Teve assistência? (s/n) ')
        if sobrenome_assistente.lower() == 's':
            sobrenome_assistente = input('Digite o sobrenome do assistente: ')
            query = f'update jogador set assistencias = assistencias + 1 where sobrenome = "{sobrenome_assistente}"'
            cursor.execute(query)
            conexao.commit()
    except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")
            conexao.rollback()

def atribuirPontos(idpartida, cursor, conexao):
    try:
        query = f'''
        select idclube1, idclube2, placarclube1, placarclube2
        from partida
        where idpartida = {idpartida};
        '''
        cursor.execute(query)
        placar = cursor.fetchone()
        
        if placar[2] > placar[3]:
            query = f'update clube set pontos = pontos + 3, jogos = jogos + 1 where idclube = {placar[0]}'
            cursor.execute(query)
            conexao.commit()

            query = f'update clube set jogos = jogos + 1 where idclube = {placar[1]}'
            cursor.execute(query)
            conexao.commit()
        
        elif placar[2] < placar[3]:
            query = f'update clube set pontos = pontos + 3, jogos = jogos + 1 where idclube = {placar[1]}'
            cursor.execute(query)
            conexao.commit()

            query = f'update clube set jogos = jogos + 1 where idclube = {placar[0]}'
            cursor.execute(query)
            conexao.commit()

        else:
            query = f'update clube set pontos = pontos + 1, jogos = jogos + 1 where idclube = {placar[0]}'
            cursor.execute(query)
            conexao.commit()

            query = f'update clube set pontos =pontos + 1, jogos = jogos + 1 where idclube = {placar[1]}'
            cursor.execute(query)
            conexao.commit()

        query = f'''
        update jogador set jogos = jogos + 1
        where idclube in (
            select idclube1 from partida where idpartida = {idpartida}
            union
            select idclube2 from partida where idpartida = {idpartida})
        '''
        cursor.execute(query)
        conexao.commit()
    except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")
            conexao.rollback()

def iniciarPartida(cursor, conexao):
    try:
        nome_campeonato = input('Digite o nome do campeonato em que a partida pertence: ')
        clube1 = input('Digite o nome do clube1: ')
        clube2 = input('Digite o nome do clube2: ')
        if clube1 == clube2:
            raise ValueError('O time não pode jogar contra si mesmo')
        query = f'''
        insert into partida (idcampeonato, idclube1, idclube2, placarclube1, placarclube2)
        values (
            (select idcampeonato from campeonato where nome = "{nome_campeonato.lower()}"),
            (select idclube from clube where nome = "{clube1.lower()}"),
            (select idclube from clube where nome = "{clube2.lower()}"),
            0, 0)
        '''

        cursor.execute(query)
        conexao.commit()
        idpartida = cursor.lastrowid
        print('Partida iniciada!')
        while True:
            query = f'''
            SELECT c1.nome, p.placarclube1, p.placarclube2, c2.nome 
            FROM partida p JOIN clube c1 
            ON p.idclube1 = c1.idclube
            JOIN clube c2
            ON p.idclube2 = c2.idclube
            WHERE p.idpartida = {idpartida};
            '''
            cursor.execute(query)
            placar_atualizado = cursor.fetchone()
            print(f'{placar_atualizado[0]} {placar_atualizado[1]} x {placar_atualizado[2]} {placar_atualizado[3]}')

            escolha = input(f'1. Registrar gol\n2. Encerrar partida\nO que deseja fazer(1 ou 2): ')
            if escolha == '1':
                marcarGol(idpartida, cursor, conexao)
            elif escolha == '2':
                print('Partida encerrada!')
                atribuirPontos(idpartida, cursor, conexao)
                break

            else:
                print('-----Digite 1 ou 2!-----')  
                continue          
    except Exception as e:
            print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")
            conexao.rollback()

def exibirDados(cursor):
    try:
        tabelas = {
            "Campeonatos": "select * from campeonato",
            "Partidas": "select * from partida",
            "Clubes": "select * from clube",
            "Jogadores": "select * from jogador"
        }

        for nome_tabela, query in tabelas.items():
            print(f"\n{'-' * 30}\n{nome_tabela.upper()}\n{'-' * 30}")
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            if resultados:
                colunas = [desc[0] for desc in cursor.description]
                print(" | ".join(colunas))  # Cabeçalho das colunas
                print("-" * 50)
                for linha in resultados:
                    print(" | ".join(map(str, linha)))
            else:
                print("Nenhum dado encontrado.")

    except Exception as e:
        print(f"Erro ao consultar os dados: {e}")

while True:
    try:
        print(f'''
        ----------O que deseja fazer?----------
        1. Criar Campeonato 
        2. Excluir Campeonato (para excluir campeonato remova todos seus clubes primeiro)
        3. Registrar Clube
        4. Excluir Clube (para excluir clube desvincule todos os jogadores antes)
        5. Adicionar Clube ao Campeonato
        6. Remover Clube do Campeonato
        7. Exibir a Tabela de classificação
        8. Iniciar Partida
        9. Registrar Jogador
        10. Excluir jogador
        11. Trocar o Jogador de Clube
        12. Adicionar Jogador ao Clube
        13. Remover Jogador do Clube
        14. Exibir estatísticas do Clube
        15. Exibir estatísticas do Jogador
        16. Encerrar!
        17. Caso não lembre de algum dado tecle 15 para consultar todos os dados cadastrados.
        ''')
       
        escolha = int(input('Digite o número da ação: '))
        if escolha == 1:
            inscreverCampeonato(cursor, conexao)
        
        elif escolha == 2:
            try:
                nome = input('Digite o nome do campeonato (Definitivo!): ')
                query_busca = f'''
                select nome
                from campeonato
                where nome = "{nome.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()
                campeonato = Campeonato(resultado[0])
                campeonato.removerCampeonato(cursor, conexao)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")
        
        elif escolha == 3:
            inscreverClube(cursor, conexao)

        elif escolha == 4:
            try:
                nome = input('Digite o nome do clube (Definitivo!): ')
                query_busca = f'''
                select nome, jogos, saldoGols, pontos
                from clube
                where nome = "{nome.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()
                clube = Clube(resultado[0], resultado[1], resultado[2], resultado[3])
                clube.removerClube(nome, cursor, conexao)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 5:
            try:
                nome = input('Digite o nome do campeonato: ')
                query_busca = f'''
                select nome
                from campeonato
                where nome = "{nome.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                campeonato = Campeonato(resultado[0])
                campeonato.adicionarClube(nome, cursor, conexao)    
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 6:
            try:
                nome = input('Digite o nome do campeonato: ')
                query_busca = f'''
                select nome
                from campeonato
                where nome = "{nome.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                campeonato = Campeonato(resultado[0])
                campeonato.removerClube(nome, cursor, conexao) 
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")
                    
        elif escolha == 7:
            try:
                nome = input('Digite o nome do campeonato: ')
                query_busca = f'''
                select nome
                from campeonato
                where nome = "{nome.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                campeonato = Campeonato(resultado[0])
                campeonato.exibirTabela(cursor)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 8:
            iniciarPartida(cursor, conexao)
        
        elif escolha == 9:
            inscreverAtleta(cursor, conexao)

        elif escolha == 10:
            try:
                sobrenome_jogador = input('Digite o sobrenome do jogador: ')
                query_busca = f'''
                select nome, sobrenome, dt_nascimento
                from jogador
                where sobrenome = "{sobrenome_jogador.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                jogador = Jogador(resultado[0], resultado[1], resultado[2])
                jogador.removerJogador(cursor, conexao)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 11:
            try:
                sobrenome_jogador = input('Digite o sobrenome do jogador: ')
                query_busca = f'''
                select nome, sobrenome, dt_nascimento
                from jogador
                where sobrenome = "{sobrenome_jogador.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                jogador = Jogador(resultado[0], resultado[1], resultado[2])
                jogador.mudarClube(sobrenome_jogador, cursor, conexao)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 12:
            try:
                sobrenome_jogador = input('Digite o sobrenome do jogador: ')
                query_busca = f'''
                select nome, sobrenome, dt_nascimento
                from jogador
                where sobrenome = "{sobrenome_jogador.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                jogador = Jogador(resultado[0], resultado[1], resultado[2])
                jogador.mudarClube(sobrenome_jogador, cursor, conexao)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 13:
            try:
                sobrenome_jogador = input('Digite o sobrenome do jogador: ')
                query_busca = f'''
                select nome, sobrenome, dt_nascimento
                from jogador
                where sobrenome = "{sobrenome_jogador}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                jogador = Jogador(resultado[0], resultado[1], resultado[2])
                jogador.demitirJogador(sobrenome_jogador, cursor, conexao)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 14:
            try:
                nome = input('Digite o nome do clube: ')
                query_busca = f'''
                select nome, jogos, saldoGols, pontos
                from clube
                where nome = "{nome.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()
                clube = Clube(resultado[0], resultado[1], resultado[2], resultado[3])
                clube.consultaClube(nome, cursor)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 15:
            try:
                sobrenome_jogador = input('Digite o sobrenome do jogador: ')
                query_busca = f'''
                select nome, sobrenome, dt_nascimento
                from jogador
                where sobrenome = "{sobrenome_jogador.lower()}"
                '''
                cursor.execute(query_busca)
                resultado = cursor.fetchone()

                jogador = Jogador(resultado[0], resultado[1], resultado[2])
                jogador.consultaAtleta(cursor)
            except Exception as e:
                print(f"Ocorreu um erro, tecle 15 se precisar de ajuda: {e}")

        elif escolha == 16:
            print(f'{"-"*15}Obrigado por utilizar nosso Software{"-"*15}')
            sOun = input('(S/N): ')
            if sOun.lower() == 's':
                print('Feito!')
                break
            elif sOun.lower() ==  'n':
                print(';)')
            else:
                print('-----Digite S ou N!!!-----')

        elif escolha == 17:
            exibirDados(cursor)

    except ValueError:
        print('Digite somente números de 1 a 12')

cursor.close()
conexao.close()