import uno
from com.sun.star.table import BorderLine

def set_gost_table_borders(*args):
    doc = XSCRIPTCONTEXT.getDocument()
    tables = doc.getTextTables()

    # толстая внешняя рамка
    outer = BorderLine()
    outer.OuterLineWidth = 30  # жирная линия

    # тонкие внутренние линии
    inner = BorderLine()
    inner.OuterLineWidth = 30  # тонкая линия

    for name in tables.getElementNames():
        table = tables.getByName(name)

        rows = table.Rows.Count
        cols = table.Columns.Count

        for i in range(rows):
            for j in range(cols):
                cell = table.getCellByPosition(j, i)

                # --- ВЕРХ ---
                if i == 0:
                    cell.TopBorder = outer
                else:
                    cell.TopBorder = inner

                # --- НИЗ ---
                if i == rows - 1:
                    cell.BottomBorder = outer
                else:
                    cell.BottomBorder = inner

                # --- ЛЕВО ---
                if j == 0:
                    cell.LeftBorder = outer
                else:
                    cell.LeftBorder = inner

                # --- ПРАВО ---
                if j == cols - 1:
                    cell.RightBorder = outer
                else:
                    cell.RightBorder = inner

    return None

# Импортируем нужное свойство для режима обтекания
from com.sun.star.text.WrapTextMode import NONE

def set_images_no_wrap(*args):
    # Получаем контекст текущего открытого документа
    doc = XSCRIPTCONTEXT.getDocument()
    
    # Получаем коллекцию всех изображений в документе
    images = doc.getGraphicObjects()

    # Проходимся по всем изображениям по их именам (как в твоем скрипте с таблицами)
    for name in images.getElementNames():
        # Получаем конкретную картинку по имени
        image = images.getByName(name)
        
        # Меняем обтекание. 
        # NONE означает "Без обтекания" (текст сверху и снизу).
        image.Surround = NONE

    return None


g_exportedScripts = (set_images_no_wrap, set_gost_table_borders,)
