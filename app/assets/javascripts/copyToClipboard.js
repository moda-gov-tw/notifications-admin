(function(Modules) {
  "use strict";

  if (!document.queryCommandSupported('copy')) return;

  Modules.CopyToClipboard = function() {

    const states = {
      'valueVisible': (options) => `
        <span class="copy-to-clipboard__value">${options.valueLabel ? '<span class="govuk-visually-hidden">' + options.thing + ': </span>' : ''}${options.value}</span>
        <span class="copy-to-clipboard__notice govuk-visually-hidden" aria-live="assertive">
          ${options.onload ? '' : options.thing + ' 回到頁面，按下按鈕複製到剪貼簿'}
        </span>
        <button type="button" class="govuk-button govuk-button--secondary copy-to-clipboard__button--copy">
          複製 ${options.thing} 到剪貼簿 ${options.name ? '<span class="govuk-visually-hidden"> 為 ' + options.name + '</span>' : ''}
        </button>
      `,
      'valueCopied': (options) => `
        <span class="copy-to-clipboard__notice" aria-live="assertive">
          <span class="govuk-visually-hidden">${options.thing} </span>已複製到剪貼簿<span class="govuk-visually-hidden">按下按鈕在頁面中顯示</span>
        </span>
        <button type="button" class="govuk-button govuk-button--secondary copy-to-clipboard__button--show">
          顯示 ${options.thing}${options.name ? '<span class="govuk-visually-hidden"> 為 ' + options.name + '</span>' : ''}
        </button>
      `
    };

    this.getRangeFromElement = function (copyableElement) {
      const range = document.createRange();
      const childNodes = Array.prototype.slice.call(copyableElement.childNodes);
      let prefixIndex = -1;

      childNodes.forEach((el, idx) => {
        if ((el.nodeType === 1) && el.classList.contains('govuk-visually-hidden')) {
          prefixIndex = idx;
        }
      });

      range.selectNodeContents(copyableElement);
      if (prefixIndex !== -1) { range.setStart(copyableElement, prefixIndex + 1); }

      return range;
    };

    this.copyValueToClipboard = function(copyableElement, callback) {
      var selection = window.getSelection ? window.getSelection() : document.selection,
          range = this.getRangeFromElement(copyableElement);

      selection.removeAllRanges();
      selection.addRange(range);
      document.execCommand('copy');
      selection.removeAllRanges();
      callback();
    };

    this.start = function(component) {

      const $component = $(component),
            stateOptions = {
              value: $component.data('value'),
              thing: $component.data('thing')
            },
            name = $component.data('name');

      // if the name is distinct from the thing:
      // - it will be used in the rendering
      // - the value won't be identified by a heading so needs its own label
      if (name !== stateOptions.thing) {
        stateOptions.name = name;
        stateOptions.valueLabel = true;
      }

      $component
        .addClass('copy-to-clipboard')
        .css('min-height', $component.height())
        .html(states.valueVisible($.extend({ 'onload': true }, stateOptions)))
        .on(
          'click', '.copy-to-clipboard__button--copy', () =>
            this.copyValueToClipboard(
              $('.copy-to-clipboard__value', component)[0], () =>
                $component
                  .html(states.valueCopied(stateOptions))
                  .find('.govuk-button').focus()
            )
        )
        .on(
          'click', '.copy-to-clipboard__button--show', () =>
            $component
              .html(states.valueVisible(stateOptions))
              .find('.govuk-button').focus()
        );

      if ('stickAtBottomWhenScrolling' in GOVUK) {
        GOVUK.stickAtBottomWhenScrolling.recalculate();
      }

    };
  };

})(window.GOVUK.NotifyModules);
