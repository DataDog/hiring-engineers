window.onload = function () {
    let getApiRoute = function(fragment) {
        let url = window.location;
        return url.protocol + '//' + url.hostname + ':55555/' + fragment;
    }

    //Lazy load iFrames
    let iframeUrls = {
        'host_metrics': 'https://p.datadoghq.com/sb/e946a7b66-593e3ffa04a653c75777e39ace0301fb',
        'used_connections': 'https://p.datadoghq.com/sb/e946a7b66-3a2b105ee8e4f7c3606e57649a65a3bd',
        'custom_metric': 'https://p.datadoghq.com/sb/e946a7b66-d90e4d3761fe1726ceac73c81710a2e5',
        'tb_one': 'https://app.datadoghq.com/graph/embed?token=84e69d827509c3bdbecb7eab92a8853992c17b6cb0152eab35dd53b15c8b3ff8&height=300&width=1200&legend=true',
        'tb_two': 'https://app.datadoghq.com/graph/embed?token=334d254e9bff9dc8c603ad5d57404005937099e195ce9872697af44a21a9b321&height=300&width=1200&legend=true',
        'tb_three': 'https://app.datadoghq.com/graph/embed?token=f47ae5499412fd2704574cbe95b81b1924089e85743f65a012255f5270fdf4a7&height=300&width=1200&legend=true',
        'nginx_metrics': 'https://p.datadoghq.com/sb/e946a7b66-44126084cf456cae0c859f22c7bfb25c',
        'monitor_dash': 'https://p.datadoghq.com/sb/e946a7b66-74e8542df6444cf85fc79195702a90f9',
        'apm_service_overview': 'https://p.datadoghq.com/sb/e946a7b66-b389d80deb1ec89734b899a75db237be',
        'apm_and_infrastructure': 'https://p.datadoghq.com/sb/e946a7b66-bb2640631907327dc233cce14477c70f'
    }

    for (let i in iframeUrls) {
        let ifr = document.getElementById(i);
        ifr.src = iframeUrls[i];
    }

    //Postgres output
    let postgresOutputBtn = document.getElementById('get_postgres_check_output');
    postgresOutputBtn.addEventListener('click', function (evt) {
        let options = { "method": "GET" , "credential": "same-origin"}
        let route = getApiRoute('postgres_check')
        fetch(route, options)
            .then(response => response.text())
            .then(responseText => {
                let contentDiv = document.getElementById('postgres_check_output');
                contentDiv.style.display = "block";
                contentDiv.innerHTML = responseText;
            })
    });

    let postgresHideOutputBtn = document.getElementById('hide_postgres_check_output');
    postgresHideOutputBtn.addEventListener('click', function (evt) {
        let contentDiv = document.getElementById('postgres_check_output');
        contentDiv.style.display = "none";
    });

    //Apm
    let logVisitorBtn = document.getElementById('log_visitor_btn');
    logVisitorBtn.addEventListener('click', function (evt) {
        let options = { "method": "GET" , "credential": "same-origin"}
        let route = getApiRoute('log_visitor')
        fetch(route, options)
            .then(response => response.json())
            .then(responseJson => {
                console.log(responseJson);
                let p = document.getElementById('apm_click_results');
                p.innerHTML = 'Hello ' + responseJson.Ip + ', you have added visitor log number ' + responseJson.Id + ' to the database.'
            })
    });

}
