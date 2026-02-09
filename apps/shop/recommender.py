import redis
from django.conf import settings
from .models import Product


# Conectarse a Redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

class Recommender:
    ''' 
    ZSET
    zincrby → aprende: suma puntos a un producto cuando se compra junto con otro (va aprendiendo asociaciones).
    zunionstore → combina gustos: junta las recomendaciones de varios productos y suma sus puntajes.
    zrem → evita repetir: quita de la recomendación los productos que ya están en el carrito.
    zrange → recomienda: devuelve los productos mejor rankeados según esas asociaciones.

    Key
    delete → limpia basura: borra claves temporales que ya no sirven (orden y memoria limpia).
    '''
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'
    

    def products_bought(self, products):
        '''
        Recibe una lista de productos comprados en una orden.
        Si alguien compra A y B juntos
        Redis guarda que A suele ir con B
        y que B suele ir con A
        '''
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # Consigue los demás productos comprados con cada producto.
                if product_id != with_id:
                    # Incrementar la puntuación por producto comprado en conjunto
                    r.zincrby(
                        self.get_product_key(product_id), 1, with_id
                    )


    def suggest_products_for(self, products, max_results=6):
        """
        Devuelve una lista de productos recomendados
        en base a compras conjuntas almacenadas en Redis.
        """
        product_ids = [p.id for p in products]

        # CASO 1: Solo un producto (vista de detalle)
        if len(products) == 1:
            # Obtener los productos más comprados junto a este producto
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]

        # CASO 2: Varios productos (carrito)
        else:
            # Crear una clave temporal única a partir de los IDs
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'

            # Obtener las claves Redis de cada producto
            keys = [self.get_product_key(id) for id in product_ids]

            # Unir todos los sorted sets y sumar sus scores
            r.zunionstore(tmp_key, keys)

            # Eliminar los productos que ya están en el carrito
            r.zrem(tmp_key, *product_ids)

            # Obtener los productos recomendados ordenados por score
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]

            # Eliminar la clave temporal
            r.delete(tmp_key)

        # Buscar en la DB 
        suggested_products_ids = [int(id) for id in suggestions]

        # Obtener los productos desde la base de datos
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))

        # Mantener el orden según el ranking de Redis
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))

        return suggested_products
    

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))



        