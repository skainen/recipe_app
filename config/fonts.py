class AppFonts:
    PRIMARY = "Rockwell"  # Modern, clean, highly readable font
    SECONDARY = "Inter"  # Good fallback option
    
    @classmethod
    def get_font_family(cls):
        return f"{cls.PRIMARY}, {cls.SECONDARY}, sans-serif"
    
    @classmethod
    def get_text_style(cls, size=14, color=None, weight=None):
        """
        Creates a consistent text style with the app's font family
        
        Args:
            size (int): Font size in pixels
            color (str): Text color
            weight (FontWeight): Text weight
            
        Returns:
            TextStyle: Configured text style
        """
        import flet as ft
        
        return ft.TextStyle(
            font_family=cls.get_font_family(),
            size=size,
            color=color,
            weight=weight,
        )