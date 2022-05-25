export const size = 10;

function typeOf(obj) {
  return obj == null ? String(obj).toLowerCase() : Object.prototype.toString.call(obj).replace(/\[object\s+(\w+)\]/i, "$1").toLowerCase() || "object";
}

export function pager(a, p) {
  return p > Math.ceil(a.length / size) ? [] : a.slice((p - 1) * size, p * size)
}

export function filter(a, o) {
  let result = [];
  a.map((v) => {
    let check = true;
    for(let i in o) {
      if(v[i]) {
        if(typeOf(v[i]) == 'string' && v[i].indexOf(o[i]) == -1) {
          check = false;
        }
        if(typeOf(v[i]) == 'object' && (o[i] === false || o[i] === 'false')) {
          check = false
        }
        if(typeOf(v[i]) == 'array' && o[i] && v[i].indexOf(o[i]) == -1) {
          check = false;
        }
      }
      else {
        if(o[i]) {
          check = false;
        }
      }
    }
    if(check) {
      result.push(v)
    }
  })
  return result;
}

export function exist(a, k, v) {
  for(let i = 0; i < a.length; i++) {
    if(a[i][k] == v) {
      return true;
    }
  }
  return false;
}

export function getSlugs(store, key) {
  let result = [];
  store.getters.data[key].map((v) => {
    result.push(v.slug);
  });
  return result;
}