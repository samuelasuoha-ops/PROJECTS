export function validateRequired(v){
  return typeof v === 'string' ? v.trim().length > 0 : false;
}
export function validateEmail(v){
  if (typeof v !== 'string') return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) && !/\.\./.test(v);
}
export function validatePassword(v){
  if (typeof v !== 'string') return false;
  return /[A-Za-z]/.test(v) && /\d/.test(v) && v.length >= 8;
}
if (typeof window !== 'undefined'){
  window.Validation = { validateRequired, validateEmail, validatePassword };
}
export default { validateRequired, validateEmail, validatePassword };
