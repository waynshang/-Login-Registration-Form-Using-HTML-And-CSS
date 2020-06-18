/**
 * 
 * @param {*} data - the  data  you want to check
 * @returns  {boolean}   -  return  true or false
 */

function  isPresent(data){
  if (data){
    switch(typeof(data)){
      case  'object':
        return Object.entries(data).length > 0;
      case 'string':
        return data.trim().length > 0;
      default:
        return true;
    }
  }
  return false
}