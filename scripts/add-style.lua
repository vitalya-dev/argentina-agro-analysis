-- Функция Blocks обрабатывает списки блоков (абзацы, таблицы, списки и т.д.)
function Blocks(blocks)
  -- Проходим по всем блокам в документе, кроме самого последнего
  for i = 1, #blocks - 1 do
    
    -- Проверяем: если текущий блок — это Таблица (Table), 
    -- а следующий за ним блок — это Абзац (Para)
    if blocks[i].t == "Table" and blocks[i+1].t == "Para" then
      
      -- Оборачиваем следующий абзац в элемент Div
      local div = pandoc.Div({blocks[i+1]})
      
      -- Назначаем этому Div атрибут пользовательского стиля
      div.attributes['custom-style'] = "AfterTableParagraph"
      
      -- Заменяем исходный абзац на новый блок Div со стилем
      blocks[i+1] = div
    end
  end
  
  return blocks
end