# Импорт кошельков

MyTonCtrl поддерживает различные типы контрактов, похожих на кошелек: wallet-v1, wallet-v3, [lockup-wallet](https://github.com/ton-blockchain/lockup-wallet-contract/tree/main/universal) и другие. Часто это самый простой способ работы с контрактом.

## Импорт через приватный ключ

Если у вас есть приватный ключ, вы можете легко импортировать кошелек. Введите следующую команду в консоль:

```
iw <адрес-кошелька> <секретный-ключ-кошелька>
```

Здесь `<секретный-ключ-кошелька>` - это ваш приватный ключ в формате base64.

## Импорт через мнемоническую фразу

Если у вас есть мнемоническая фраза (последовательность из 24 слов, например, `tattoo during ...`), следуйте этим шагам:

1. Установите Node.js.
2. Клонируйте и установите [mnemonic2key](https://github.com/ton-blockchain/mnemonic2key):
    ```
    git clone https://github.com/ton-blockchain/mnemonic2key.git
    cd mnemonic2key
    npm install
    ```
3. Запустите следующую команду, замените `word1`, `word2`... на вашу мнемоническую фразу и `address` на адрес вашего контракта кошелька:
    ```
    node index.js word1 word2 ... word24 [address]
    ```
4. Скрипт сгенерирует `wallet.pk` и `wallet.addr`. Переименуйте их в `imported_wallet.pk` и `imported_wallet.addr`.
5. Скопируйте оба файла в каталог `~/.local/share/mytoncore/wallets/`.
6. Откройте консоль mytonctrl и перечислите кошельки с помощью команды `wl`.
7. Убедитесь, что кошелек был импортирован и отображает правильный баланс.
8. Теперь вы можете отправить средства с помощью команды `mg`. Введите `mg`, чтобы просмотреть справочную документацию.
Помните, что при выполнении команд следует заменить заполнители (слова внутри `< >`) на ваши фактические значения.
