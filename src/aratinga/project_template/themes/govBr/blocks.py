from django import forms
from wagtail import blocks

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class CustomParagraphBlock(blocks.StructBlock):

    paragraph = blocks.RichTextBlock()

    class Meta:
        icon = 'pilcrow'
        verbose_name = 'Bloco de Parágrafo'
        help_text = 'Um bloco para adicionar um parágrafo personalizado.'


class ImageBlock(blocks.StructBlock):
    """
    `StructBlock` personalizado para utilizar imagens com legenda associada e
    dados de atribuição
    """ 

    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False)
    attribution = blocks.CharBlock(required=False)

    class Meta:
        verbose_name = "Bloco de Imagem"
        icon = "image"
        template = "blocks/image_block.html"


class BlockQuote(blocks.StructBlock):
    """
    Custom `StructBlock` que permite ao usuário atribuir uma citação ao autor
    """

    text = blocks.TextBlock()
    attribute_name = blocks.CharBlock(blank=True, required=False, label="por exemplo. Fulano da Silva")

    class Meta:
        verbose_name = "Bloco de Citação"
        icon = "openquote"
        template = "blocks/blockquote.html"


# Blocos de encaixe
class BaseStreamBlock(blocks.StreamBlock):
    """
    Defina os blocos personalizados que `StreamField` utilizará
    """

    paragraph_block = blocks.RichTextBlock(
        label="Texto Rico",
        help_text='Utilize quebras de linha, negrito, itálico, listas e formatação de links para tornar seu texto mais organizado e legível.',
        icon="doc-full", template="blocks/paragraph_block.html"
    )
    table_block = TableBlock(label="Tabela", group="Conteúdo")
    typed_table_block = TypedTableBlock(
        [
            ("text", blocks.CharBlock()),
            ("numeric", blocks.FloatBlock()),
            ("rich_text", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        group="Conteúdo", label="Tabela Tipada",
    )
    embed_block = EmbedBlock(
        label="Incorporar",
        help_text="Insira um URL de incorporação e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="blocks/embed_block.html",
    )

    class Meta:
        verbose_name = "Bloco de Incorporação"



