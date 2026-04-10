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


g_exportedScripts = (set_gost_table_borders,)
