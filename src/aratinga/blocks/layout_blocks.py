"""
Layout blocks are essentially a wrapper around content.
e.g. rows, columns, hero units, etc.
"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from aratinga.settings import cms_settings

from .base_blocks import BaseLayoutBlock


# Level 1 layout blocks


class ColumnBlock(BaseLayoutBlock):
    """
    Renders content in a column.
    """

    column_size = blocks.ChoiceBlock(
        choices=cms_settings.CMS_FRONTEND_COL_SIZE_CHOICES,
        default=cms_settings.CMS_FRONTEND_COL_SIZE_DEFAULT,
        required=False,
        label=_("Column size"),
    )


    class Meta:
        template = "aratinga/blocks/column_block.html"
        icon = "placeholder"
        label = "Column"


class GridBlock(BaseLayoutBlock):
    """
    Renders a row of columns.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        label=_("Full width"),
    )

    class Meta:
        template = "aratinga/blocks/grid_block.html"
        icon = "ara-columns"
        label = _("Responsive Grid Row")

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks=[("content", ColumnBlock(local_blocks))])


class CardGridBlock(BaseLayoutBlock):
    """
    Renders a row of cards.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        label=_("Full width"),
    )

    class Meta:
        template = "aratinga/blocks/cardgrid_deck.html"
        icon = "ara-th-large"
        label = _("Card Grid")


class HeroBlock(BaseLayoutBlock):
    """
    Wrapper with color and image background options.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Full width"),
    )
    is_parallax = blocks.BooleanBlock(
        required=False,
        label=_("Parallax Effect"),
        help_text=_(
            "Background images scroll slower than foreground images, creating an illusion of depth."
        ),
    )
    background_image = ImageChooserBlock(required=False)
    tile_image = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Tile background image"),
    )
    background_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Background color"),
        help_text=_("Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)"),
    )
    foreground_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Text color"),
        help_text=_("Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)"),
    )

    class Meta:
        template = "aratinga/blocks/hero_block.html"
        icon = "ara-newspaper-o"
        label = "Hero Unit"
