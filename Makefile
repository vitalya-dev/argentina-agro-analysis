# =========================
# Настройки путей и имен
# =========================

# Имена исходных файлов (без расширения)
SRC = Arg_Agro_Report
PRESENT = Arg_Agro_Deck

# Папки
BUILD_DIR = build
TEMPLATE_DIR = templates

# Выходные файлы
ODT = $(BUILD_DIR)/$(SRC).odt
PPT = $(BUILD_DIR)/$(PRESENT).pptx

# Шаблоны
TEMPLATE_ODT = $(TEMPLATE_DIR)/Template.odt
TEMPLATE_PPT = $(TEMPLATE_DIR)/Template.pptx

# Pandoc и фильтры
PANDOC = pandoc
FILTERS = --filter pandoc-crossref

# =========================
# Основные цели
# =========================

all: directories odt ppt

# Создание папки build, если ее нет
directories:
	mkdir -p $(BUILD_DIR)

odt: directories $(ODT)
ppt: directories $(PPT)

# =========================
# Сборка ODT
# =========================

$(ODT): blank.md $(SRC).md
	$(PANDOC) $^ -o $@ \
	$(FILTERS) \
	--citeproc \
	--reference-doc=$(TEMPLATE_ODT) \
	--toc \
	--table-caption-position=below

# =========================
# Сборка презентации PPTX
# =========================

$(PPT): $(PRESENT).md
	$(PANDOC) $< -o $@

# =========================
# Очистка
# =========================

clean:
	rm -rf $(BUILD_DIR)/*.odt $(BUILD_DIR)/*.pptx $(BUILD_DIR)/*.pdf

# Пересборка
rebuild: clean all