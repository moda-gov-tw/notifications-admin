json2po ./assets/i18n/zh_Hant_TW/translation.json --pot ./js.pot
msgcat ./js.pot ./messages.pot > ./messages_js.pot
pybabel update --no-fuzzy-matching -l zh_hant_TW -d ./locales -i messages_js.pot
pybabel update --no-fuzzy-matching -l en -d ./locales -i messages_js.pot
po2json -t ./assets/i18n/en/translation.json ./locales/zh_Hant_TW/LC_MESSAGES/messages.po ./assets/i18n/en/translation.json
