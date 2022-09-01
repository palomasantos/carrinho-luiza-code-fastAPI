cart = []
all_cars = []
def add_item_cart(item, carrinho):
    cart.append(item)
    return cart

def get_all_items_cart(all_cars, cart):
    for i in cart:
        all_cars.append(i[1])
    return all_cars

# def get_item_cart_by_id(id_produto):
#     return

def remove_item_id(remove_item,cart):
    for i in cart:
        if i[1] == remove_item:
            cart.remove(i) 
    return cart
#remover o item do carrinho que tem esse produto
#     pass


def execut():
    quantity_total = int(input('Quantos produtos você deseja comprar?'))
    id_user = input("Insira o id do usuário:")
    for i in range(quantity_total):
        id_produto = input("Insira o id do produto:")
        price_product = float(input("Insira o preço do produto:"))
        quantity_product = int(input("Insira a quantidade de produto:"))
        item = [id_user, id_produto, price_product, quantity_product]
        add_item_cart(item, cart)

    print(list(cart))
    get_all_items_cart(all_cars, cart)
    print(all_cars)
    remove_item = input("Insira o id do produto que você deseja remover:")
    remove_item_id(remove_item, cart)
    print(cart)

execut()



# def remove_item_id(id_product):
#     #remover o item do carrinho que tem esse produto
#     pass