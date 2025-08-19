import * as Validation from '../js/validation.js';

describe('validation utilities', () => {
  test('validateRequired', () => {
    expect(Validation.validateRequired('hello')).toBe(true);
    expect(Validation.validateRequired('  spaced  ')).toBe(true);
    expect(Validation.validateRequired('')).toBe(false);
    expect(Validation.validateRequired('   ')).toBe(false);
    expect(Validation.validateRequired(null)).toBe(false);
    expect(Validation.validateRequired(undefined)).toBe(false);
  });

  test('validateEmail', () => {
    const valids = ['user@example.com','first.last@sub.domain.co.uk','user+alias@domain.io'];
    const invalids = ['','plain','@nouser.com','user@.nodomain','user@domain,com','user@domain','user@domain..com'];
    valids.forEach(e => expect(Validation.validateEmail(e)).toBe(true));
    invalids.forEach(e => expect(Validation.validateEmail(e)).toBe(false));
  });

  test('validatePassword (>=8 chars, letters+digits)', () => {
    const good = ['password1','A1b2c3d4','2LongEnoughx'];
    const bad  = ['short1','nonumbers','12345678','',null,undefined];
    good.forEach(p => expect(Validation.validatePassword(p)).toBe(true));
    bad.forEach(p => expect(Validation.validatePassword(p)).toBe(false));
  });
});
