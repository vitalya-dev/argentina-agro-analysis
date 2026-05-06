from com.sun.star.table import BorderLine
from com.sun.star.text.WrapTextMode import NONE
from com.sun.star.style.ParagraphAdjust import CENTER

def center_special_headings(*args):
    """Центрирует ВВЕДЕНИЕ, ЗАКЛЮЧЕНИЕ и другие структурные заголовки без изменения их уровня"""
    doc = XSCRIPTCONTEXT.getDocument()
    
    # Список заголовков, которые нужно выровнять по центру (можешь добавить свои)
    target_headings = [
        "ВВЕДЕНИЕ", 
        "ЗАКЛЮЧЕНИЕ", 
        "СПИСОК ИСПОЛЬЗОВАННОЙ ЛИТЕРАТУРЫ",
        "ПРИЛОЖЕНИЕ А"
    ]
    
    text = doc.getText()
    paragraphs = text.createEnumeration()
    
    while paragraphs.hasMoreElements():
        para = paragraphs.nextElement()
        
        # Проверяем, что текущий элемент — это абзац (заголовки тоже являются абзацами)
        if para.supportsService("com.sun.star.text.Paragraph"):
            # Читаем текст и убираем случайные пробелы по краям
            current_text = para.getString().strip()
            
            # Если текст абзаца совпадает с нужными нам
            if current_text in target_headings:
                # Просто выравниваем его по центру! 
                # (Стиль остается Heading 1, поэтому оглавление не сломается)
                para.ParaAdjust = CENTER
                
                # Если вдруг ты всё же хочешь применить именно свой стиль из шаблона,
                # закомментируй строку выше и раскомментируй строку ниже:
                # para.ParaStyleName = "HeadingCenter"
                
    return None

def update_table_of_contents(*args):
    """Обновляет все оглавления и списки в документе"""
    doc = XSCRIPTCONTEXT.getDocument()
    
    # Получаем все индексы (оглавления) в документе
    indexes = doc.getDocumentIndexes()
    
    # Проходимся по всем найденным оглавлениям и обновляем их
    for i in range(indexes.getCount()):
        index = indexes.getByIndex(i)
        index.update()
        
    return None

def set_page_margins(*args):
    """Устанавливает поля: 2 см сверху/снизу, 3 см слева, 1.5 см справа"""
    doc = XSCRIPTCONTEXT.getDocument()
    style_families = doc.StyleFamilies
    page_styles = style_families.getByName("PageStyles")
    standard_style = page_styles.getByName("Standard")
    
    # Задаем поля в сотых долях миллиметра (1 см = 1000)
    standard_style.TopMargin = 2000    
    standard_style.BottomMargin = 2000 
    standard_style.LeftMargin = 3000   
    standard_style.RightMargin = 1500  
    
    return None

def set_gost_table_borders(*args):
    """Делает толстую внешнюю и тонкую внутреннюю рамку у всех таблиц"""
    doc = XSCRIPTCONTEXT.getDocument()
    tables = doc.getTextTables()

    outer = BorderLine()
    outer.OuterLineWidth = 30  

    inner = BorderLine()
    inner.OuterLineWidth = 30  

    for name in tables.getElementNames():
        table = tables.getByName(name)
        rows = table.Rows.Count
        cols = table.Columns.Count

        for i in range(rows):
            for j in range(cols):
                cell = table.getCellByPosition(j, i)

                # ВЕРХ
                if i == 0: cell.TopBorder = outer
                else: cell.TopBorder = inner

                # НИЗ
                if i == rows - 1: cell.BottomBorder = outer
                else: cell.BottomBorder = inner

                # ЛЕВО
                if j == 0: cell.LeftBorder = outer
                else: cell.LeftBorder = inner

                # ПРАВО
                if j == cols - 1: cell.RightBorder = outer
                else: cell.RightBorder = inner

    return None

def set_images_no_wrap(*args):
    """Убирает обтекание текстом у всех изображений"""
    doc = XSCRIPTCONTEXT.getDocument()
    images = doc.getGraphicObjects()

    for name in images.getElementNames():
        image = images.getByName(name)
        image.Surround = NONE

    return None


# --- ГЛАВНАЯ КНОПКА (ОБЩАЯ ФУНКЦИЯ) ---
def format_all_elements(*args):
    """Запускает форматирование полей, таблиц, картинок, заголовков и обновляет оглавление разом"""
    
    set_page_margins()
    set_gost_table_borders()
    set_images_no_wrap()
    
    # Шаг 3.5: Центрируем Введение и Заключение
    center_special_headings()
    
    # Шаг 4: Обновляем оглавление
    update_table_of_contents()
    
    return None

# Регистрируем все функции
g_exportedScripts = (
    format_all_elements,  
    update_table_of_contents,  
    set_page_margins,  
    set_gost_table_borders,  
    set_images_no_wrap,
    center_special_headings, # <-- Не забудь добавить сюда!
)