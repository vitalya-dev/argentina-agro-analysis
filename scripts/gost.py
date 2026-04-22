import uno
from com.sun.star.table import BorderLine
from com.sun.star.text.WrapTextMode import NONE

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
    """Запускает форматирование полей, таблиц, картинок и обновляет оглавление разом"""
    
    # Шаг 1: Настраиваем поля документа
    set_page_margins()
    
    # Шаг 2: Применяем рамки ГОСТ к таблицам
    set_gost_table_borders()
    
    # Шаг 3: Убираем обтекание у картинок
    set_images_no_wrap()
    
    # Шаг 4: Обновляем оглавление (обязательно в самом конце!)
    update_table_of_contents()
    
    return None


# Регистрируем все функции
g_exportedScripts = (
    format_all_elements, 
    update_table_of_contents, 
    set_page_margins, 
    set_gost_table_borders, 
    set_images_no_wrap,
)