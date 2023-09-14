import bcrypt

class BcryptUtil:
    @staticmethod
    def gerar_salt():
        """
        Gera um salt aleatório para uso com o bcrypt.

        Retorna:
            bytes: O salt gerado.
        """
        return bcrypt.gensalt()

    @staticmethod
    def hash_senha(senha,salt):
        """
        Hashes a senha fornecida usando o salt especificado.

        Parâmetros:
            senha (str): A senha a ser hash.
            salt (bytes): O salt a ser usado para hashing.

        Retorna:
            bytes: O hash da senha.
        """
        senha_ = senha.encode('utf-8')
        return bcrypt.hashpw(senha_,salt)

    @staticmethod
    def verificar_senha(senha,hash_armazenado,salt):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado usando o salt especificado.

        Parâmetros:
            senha (str): A senha a ser verificada.
            hash_armazenado (bytes): O hash armazenado que será verificado.
            salt (bytes): O salt usado para o hash armazenado.

        Retorna:
            bool: True se a senha corresponder ao hash armazenado, False caso contrário.
        """
        hash_senha_ = BcryptUtil.hash_senha(senha,salt)
        return hash_senha_ == hash_armazenado
