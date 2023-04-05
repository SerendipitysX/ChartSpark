import axios from 'axios';

const T_URL = 'http://127.0.0.1:88';

export function sendChart(param, callback) {
    const url = `${T_URL}/setting1`;
    axios.post(url, param)
    .then(response => {
        console.log("preview & theme OK")
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

export function startGenerate(param, callback) {
    const url = `${T_URL}/generate_element`;
    axios.post(url, param)
    .then(response => {
        console.log("Generate OK")
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}
