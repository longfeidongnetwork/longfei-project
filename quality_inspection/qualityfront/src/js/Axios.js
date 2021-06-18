// axios 配置
import axios from 'axios'
import router from '../router'
// axios 全局配置
// axios.defaults.baseURL = 'http://127.0.0.1:8000/';
axios.defaults.baseURL = 'http://61.147.15.39:18094/';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true
// 请求拦截
axios.interceptors.request.use(
    config =>{
        // 想要获取的cook键值
        var username = "username";
        var cookie_value = getCookie(username);
        if (cookie_value){
            // 若存在token，则在每个Http Header都加上token
            config.headers.Authorization = `token=${cookie_value}`
        }
        // console.log('request请求配置',config)
        return config
    },
    err =>{
        return Promise.reject(err)
    }
)
// 响应拦截
axios.interceptors.response.use(function(res) {
        // console.log('成功响应:',res)
        if(res.data.code === '301'){
            router.push({
                path: "/"
            });
        }else{
            return res   
        }   
    },
    error => {
        if(error.response){
            console.log(error.response)
        }
        // 返回接口返回的错误信息
        return Promise.reject(error.response)
    }
)

function getCookie(username) {
    var allcookies = document.cookie;
    //索引长度，开始索引的位置
    var cookie_pos = allcookies.indexOf(username);

    // 如果找到了索引，就代表cookie存在,否则不存在
    if (cookie_pos != -1) {
        // 把cookie_pos放在值的开始，只要给值加1即可
        //计算取cookie值得开始索引，加的1为“=”
        cookie_pos = cookie_pos + username.length + 1; 
        //计算取cookie值得结束索引
        var cookie_end = allcookies.indexOf(";", cookie_pos);
        
        if (cookie_end == -1) {
            cookie_end = allcookies.length; 
        }
        //得到想要的cookie的值
        var value = unescape(allcookies.substring(cookie_pos, cookie_end)); 
    }
    return value;
}
export default axios