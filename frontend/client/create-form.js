/*
** create-form.js
*/

const ENTER_KEY_CODE = 13;
const HOST = window.location.hostname;

class CreateForm {
  constructor(repository) {
    this._repository = repository;
    this._input = document.querySelector('.create-form__input');
    this._button = document.querySelector('.create-form__button');
    this._link = document.querySelector('.create-form__link');
  }

  runListeners() {
    this._button.addEventListener('click', () => {
      this._saveLink(this._input.value);
    });

    this._input.addEventListener('keydown', (event) => {
      if (event.keyCode === ENTER_KEY_CODE) {
        this._saveLink(this._input.value);
      }
    });
  }

  _saveLink(url) {
    if (!url.length) {
      return;
    }

    this._repository.save({ url }).then((link) => {
      this._link.textContent = `${HOST}/${link.key}`;
      this._link.href = link.key;
    });
  }
}

exports.CreateForm = CreateForm;
