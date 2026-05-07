-- Функция Blocks обрабатывает списки блоков (абзацы, таблицы, списки и т.д.)
function Blocks(blocks)
  local new_blocks = {}
  
  for i = 1, #blocks do
    local current = blocks[i]
    local next_block = blocks[i+1]
    
    -- 1. Логика для "LastParagraph" (абзац перед заголовком или последний в документе)
    if current.t == "Para" then
      if next_block == nil or next_block.t == "Header" then
        local div = pandoc.Div({current})
        div.attributes['custom-style'] = "LastParagraph"
        current = div
      end
    end
    
    -- 2. Логика для "AfterTableParagraph" (абзац сразу после таблицы)
    -- Если текущий блок - Таблица, а следующий - Абзац, то мы пометим СЛЕДУЮЩИЙ в его итерации
    -- Но проще проверить: если текущий Абзац идет ПОСЛЕ Таблицы
    if current.t == "Para" or (current.t == "Div" and current.content[1] and current.content[1].t == "Para") then
      local prev_block = blocks[i-1]
      if prev_block and prev_block.t == "Table" then
        -- Если он уже в Div (от LastParagraph), просто добавим/заменим стиль
        if current.t == "Div" then
          current.attributes['custom-style'] = "LastParagraphAfterTable" -- Можно сделать комбинированный стиль
        else
          local div = pandoc.Div({current})
          div.attributes['custom-style'] = "AfterTableParagraph"
          current = div
        end
      end
    end
    
    table.insert(new_blocks, current)
  end
  
  return new_blocks
end