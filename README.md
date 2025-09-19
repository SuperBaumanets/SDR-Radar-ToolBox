# Проект: Система управления и обработки сигналов для SDR (Software Defined Radio)

## Описание проекта

Данный проект представляет собой систему для работы с программно-определяемыми радиомодулями (SDR). Приложение обеспечивает взаимодействие с аппаратными компонентами через интерфейс IIO (Industrial I/O), предоставляя возможности для:

- Настройки и управления радиомодулями (например, AD9361)
- Передачи RF-сигналов
- Обработки сигналов в реальном времени
- Интеграции с различными SDR
- Расчет параметров локаторного оборудования

## Установка зависимостей для работы с ADI-устройствами

#### Предварительные требования

Перед установкой убедитесь, что ваша система обновлена:
```bash
sudo pacman -Syu
```

#### Основные зависимости

Установите необходимые системные пакеты:

```bash
sudo pacman -S --needed base-devel git libxml2 bison flex cmake python-pip libusb avahi libaio
```

#### Установка CDK (через AUR)

Для установки CDK потребуется AUR
```bash
yay -S cdk
```

#### Установка libiio

```bash
cd ~
git clone --branch v0.23 https://github.com/analogdevicesinc/libiio.git
cd libiio
mkdir build
cd build
cmake -DPYTHON_BINDINGS=ON ..
make -j$(nproc)
sudo make install
sudo ldconfig
```

#### Установка libad9361-iio

```bash
cd ~
git clone https://github.com/analogdevicesinc/libad9361-iio.git
cd libad9361-iio
mkdir build
cd build
cmake ..
make -j$(nproc)
sudo make install
```

#### Установка pyadi-iio

```bash
cd ~
git clone --branch v0.0.14 https://github.com/analogdevicesinc/pyadi-iio.git
cd pyadi-iio
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
sudo python setup.py install
```

## Запуск проекта

### Предварительные требования

Перед запуском убедитесь, что выполнены все шаги по установке зависимостей, перечисленные в предыдущем разделе.

### Установка и запуск с использованием Poetry

1. **Активация виртуального окружения и установка зависимостей**:

```bash
# Установка Poetry (если не установлен)
curl -sSL https://install.python-poetry.org | python3 -

# Переход в директорию проекта
cd path/to/your/project

# Установка зависимостей (указанных в pyproject.toml)
poetry install

# Активация виртуального окружения
poetry shell
```

2. **Запуск приложения**:

```bash
# Основной скрипт
python main.py

# Или с использованием Poetry
poetry run python main.py
```

### Альтернативный запуск с использованием pip

Если вы предпочитаете использовать pip вместо Poetry:

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate     # Для Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python main.py
```