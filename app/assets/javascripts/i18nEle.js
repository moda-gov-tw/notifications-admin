(function(window) {
  "use strict";

  i18next.init({
    lng: 'zh_Hant_TW',
    debug: true,
    resources: {
      zh_Hant_TW: {
        translation: {
          "hello": "嗨！"
        }
      }
    }
  }, (err, t) => {
    if (err) return console.log('something went wrong loading', err);
    window.GOVUK.i18next = t;
  });

  //window.GOVUK.i18n = Translator.init({
  //  availableLangs: ['zh_Hant_TW'],
  //  defaultLanguage: 'zh_Hant_TW',
  //  isLocalValuesAllowed: true,
  //  isEnableAttr: false,
  //  assetsLocation: 'assets/i18n'
  //});

  //window.GOVUK.i18n = new I18n({
  //  locales: ['en', 'de'],
  //  directory: path.join(__dirname, 'locales')
  //});
})(window);
