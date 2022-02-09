/*! DSFR v1.2.1 | SPDX-License-Identifier: MIT | License-Filename: LICENSE.md | restricted use (see terms and conditions) */

const config = {
  prefix: 'fr',
  namespace: 'dsfr',
  organisation: '@gouvfr',
  version: '1.2.1'
};

const api = window[config.namespace];

class ToggleInput extends api.core.Instance {
  static get instanceClassName () {
    return 'ToggleInput';
  }

  get isChecked () {
    return this.getAttribute('checked');
  }
}

class ToggleStatusLabel extends api.core.Instance {
  static get instanceClassName () {
    return 'ToggleStatusLabel';
  }

  init () {
    this.register(`input[id="${this.getAttribute('for')}"]`, ToggleInput);
    this.update();
  }

  get proxy () {
    const scope = this;
    return Object.assign(super.proxy, {
      update: scope.update.bind(scope)
    });
  }

  get input () {
    return this.getRegisteredInstances('ToggleInput')[0];
  }

  update () {
    const checked = this.input.isChecked;
    const style = getComputedStyle(this.node, 'before');
    let maxWidth = parseInt(style.width);
    this.input.node.checked = !checked;

    const style2 = getComputedStyle(this.node, 'before');
    const width = parseInt(style2.width);
    if (width > maxWidth) maxWidth = width;
    this.input.node.checked = checked;

    this.node.style = '--toggle-status-width:' + (maxWidth / 16) + 'rem';
  }
}

const ToggleSelector = {
  STATUS_LABEL: `${api.internals.ns.selector('toggle__label')}${api.internals.ns.attr.selector('checked-label')}${api.internals.ns.attr.selector('unchecked-label')}`
};

// import { ToggleInput } from './script/toggle/toggle-input.js';

api.toggle = {
  ToggleStatusLabel: ToggleStatusLabel,
  ToggleSelector: ToggleSelector
};

api.internals.register(api.toggle.ToggleSelector.STATUS_LABEL, api.toggle.ToggleStatusLabel);
//# sourceMappingURL=toggle.module.js.map
