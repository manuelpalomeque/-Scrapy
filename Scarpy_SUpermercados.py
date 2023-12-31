# Para este proyecto, busco extraer los datos del producto y del precio del mismo de la pagina web de Hiper Libertad:
# https://www.hiperlibertad.com.ar/

# 01 - Importo librerias necesarias:
import scrapy
from datetime import datetime

# 02-  Configuro el la fecha actual:
hora = datetime.now().time()
fecha = datetime.now().today()

#03- Formato correcto para la fecha y hora:
fHoraMinuto = "%H:%M"
fDiaMesAño = "%d-%m-%Y"

horaActual = hora.strftime(fHoraMinuto)
fechaActual = fecha.strftime(fDiaMesAño)

# prueba de resultado:
# print(f'''
# La fecha actual es: {fechaActual}
# La hora actual es: {horaActual}''')

# 04 - Configuro la araña:

class ProductosSpider(scrapy.Spider):
    name = 'Canasta'
    start_urls = [
        "https://www.hiperlibertad.com.ar/pan-frances-x-500-g/p",
        "https://www.hiperlibertad.com.ar/galletita-cracker-la-providencia-clasica-x303g/p",
        "https://www.hiperlibertad.com.ar/galletas-terrabusi-variedad-dorada-x-300-gr/p",
        "https://www.hiperlibertad.com.ar/arroz-parboil-taeq-240gr/p",
        "https://www.hiperlibertad.com.ar/harina-de-trigo-morixe-000-1-kg/p",
        "https://www.hiperlibertad.com.ar/fideos-tallarines-n7-matarazzo-x-500-gr/p",
        "https://www.hiperlibertad.com.ar/papa-cepillada-x-1-kg/p",
        "https://www.hiperlibertad.com.ar/batata-x-500-g/p",
        "https://www.hiperlibertad.com.ar/azucar-azucel-1-kilo/p",
        "https://www.hiperlibertad.com.ar/mermelada-dulcor-durazno-frasco-454-gr/p",
        "https://www.hiperlibertad.com.ar/lentejas-taeq-200gr/p",
        "https://www.hiperlibertad.com.ar/arvejas-montenevi-x-340-gr/p",
        "https://www.hiperlibertad.com.ar/acelga-congelada-green-life-500-g/p",
        "https://www.hiperlibertad.com.ar/cebolla-x-500-g/p",
        "https://www.hiperlibertad.com.ar/bandeja-lechuga-mantecosa-lavada-sue-o-verde-x-200-gr/p",
        "https://www.hiperlibertad.com.ar/tomate-perita-x-500g/p",
        "https://www.hiperlibertad.com.ar/calabacin-anquito-fraccionado-x-700gr-1-2-calabacin/p",
        "https://www.hiperlibertad.com.ar/mandarina-x-1kg/p",
        "https://www.hiperlibertad.com.ar/naranja-p-jugo-x-1kg/p",
        "https://www.hiperlibertad.com.ar/banana-x-kg-ecomm/p",
        "https://www.hiperlibertad.com.ar/pollo-fresco-x-un-aprox-2-5kg/p",
        "https://www.hiperlibertad.com.ar/pulpa-de-jamon-de-cerdo-x-500-g/p",
        "https://www.hiperlibertad.com.ar/milanesa-de-bola-de-lomo-de-novillito-x-500-g/p",
        "https://www.hiperlibertad.com.ar/huevo-blanco-carnave-carton-x-12-unidades/p",
        "https://www.hiperlibertad.com.ar/leche-entera-c-calcio-la-lacteo-larga-vida-1-l/p",
        "https://www.hiperlibertad.com.ar/manteca-tonadita-200gr/p",
        "https://www.hiperlibertad.com.ar/aceite-de-girasol-alsamar-x-900-ml/p",
        "https://www.hiperlibertad.com.ar/brahma-chopp-can-4x6-473cc/p",
        "https://www.hiperlibertad.com.ar/sal-fina-dos-anclas-250-gr/p",
        "https://www.hiperlibertad.com.ar/mayonesa-hellmanns-clasica-x-475-gr/p",
        "https://www.hiperlibertad.com.ar/cafe-molido-bonafide-sensaciones-torrado-intenso-500-gr/p",
        "https://www.hiperlibertad.com.ar/yerba-playadito-suave-bcp-1kg/p",
    ]


    # 05 - Configuro la funcion Parse:

    # Este parse no funciono porque tenia mal  la etiqueta del nombre y porque el producto lo tenia configurado como si
    # buscara por varias paginas, pero al final le di las paginas puntuales donde buscar, pero lo dejo para comprender el
    # error:
    # def parse(self, response):
    #     for span in response.css("div.pr0 items-stretch vtex-flex-layout-0-x-stretchChildrenWidth flex"):
    #         yield {
    #             "fecha": fechaActual,
    #             "hora": horaActual,
    #             #"pagina": response.css("li.next a::attr(href)").get(),
    #             "Producto": response.css("span.vtex-store-components-3-x-productBrand::text").get(),
    #         }

    def parse(self, response):
        # Utilizando expresiones CSS
        nombre_producto = response.css('span.vtex-store-components-3-x-productBrand::text').get()
        # El precio esta dividido en 3 span diferentes (miles, cientos, centavos)
        precio_producto_miles = response.css("span.vtex-product-price-1-x-currencyInteger::text").getall()
        #precio_producto_cientos = response.css("span.vtex-product-price-1-x-currencyInteger::text").get()
        precio_producto_decimales =  response.css("span.vtex-product-price-1-x-currencyFraction::text").get()
        if len(precio_producto_miles) == 1:
            precio = precio_producto_miles # cuando el producto vale cientos
        elif len(precio_producto_miles[0])> 1:
            precio = precio_producto_miles[1] # cuando el producto tiene un precio anterior, enfatizando una oferta
        else:
            precio = f'{precio_producto_miles[0]}.{precio_producto_miles[1]}' # cuando vale miles y cientos
        yield {
            "fecha": fechaActual,
            "hora": horaActual,
            "Nombre Producto": nombre_producto,
            # El precio esta dividido en 3 span diferentes (miles, cientos, centavos), por eso los contateno:
            "Precio": precio,
            #"Precio": f"{precio},{precio_producto_decimales}"
            # No logro diferenciar los divs de miles de lo que corresponde a los cientos
            #"pagina": ProductosSpider.start_urls,  ME TRAE EL LISTADO COMPLETO DE PAGINAS NO LA QUE USA EN EL MOMENTO
        }

# 06 - Extrer los datos:
# En la terminal, sobre la carpeta en la que esta guardado el codigo, hay que ejecutar el siguiente comando:
# scrapy runspider Scarpy_SUpermercados.py -o productos.csv