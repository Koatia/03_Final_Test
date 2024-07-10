#!/bin/bash

# Добавление удаленных репозиториев
git remote add origin git@github.com:Koatia/03_Final_Test.git;
git remote add mirror ssh://git@gitverse.ru:2222/Kostia/03_Final_Test.git

# Пуш изменений в оба репозитория
git push origin master; git push mirror master

echo '--------'

git status

echo '--------'

echo "Обновление завершено, нажмите ENTER"
read tem
