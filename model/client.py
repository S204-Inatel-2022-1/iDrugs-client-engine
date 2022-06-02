
class Client:
    def __init__(self, name, email, password, photo_link, cpf, last_name, street, number, neighborhood, complement, city):
        self.name = name
        self.last_name = last_name
        self.cpf = cpf
        self.email = email
        self.password = password
        self.photo_link = photo_link
        self.street = street
        self.number = number
        self.neighborhood = neighborhood
        self.complement = complement
        self.city = city

    def imprimi(self):
        print(f"Nome: {self.name}")
        print(f"Sobrenome: {self.last_name}")
        print(f"Email: {self.email}")
        print(f"Rua: {self.street}")
        print(f"Número: {self.number}")
        print(f"Bairro: {self.neighborhood}")
        print(f"Complemento: {self.complement}")
        print(f"Cidade: {self.city}")
        print(f"Password: {self.password}")
        print(f"Link Foto: {self.photo_link}")