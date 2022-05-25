import request from '@/utils/request'

export function getData() {
  return request({
    url: `https://eefocus-static.eefcdn.com/promotion/module/data/data.json?t=${(new Date()).getTime()}`,
    method: 'get'
  })
}

export function setData(data) {
  return request({
    method: 'post',
    url: 'https://www.cirmall.com/api/eef_ads_sys/update',
    data: {data: data}
  })
}