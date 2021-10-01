var selectedFile;
window.addEventListener('load', async () => {

    // Modern dapp browsers...
    if (window.ethereum) {
        initCrossAjax();
        window.web3 = new Web3(ethereum);
        try {
            console.log("KKKKK")
            // Request account access if needed
            await ethereum.enable();
            // Acccounts now exposed
            let accounts = await web3.eth.getAccounts();
            if (accounts.length !== 0) {
                // update balances
                await updateUI(accounts[0]);
                // start account change listener
                checkAccountChange();
                // // start metamask locked/unlocked listener
                // checkMetamaskUnlocked();
                // check ethereum network
                checkEthereumNetwork();
            } else {
                // Metamask is locked need to login again
                disconnectMetamask();
            }
        } catch (error) {
            console.log(error);
            // User denied account access...
        }
    }
    // Legacy dapp browsers...
    else if (window.web3) {
        window.web3 = new Web3(web3.currentProvider);
    }
    // Non-dapp browsers...
    else {
        console.log('Non-Ethereum browser detected. You should consider trying MetaMask!');
    }


    // file selector
    checkBrowserIsSupportFileSelect();

    document.getElementById("keystoreFile").addEventListener("change", function () {
        var file = this.files[0];
        selectedFile = file;
        if (file) {
            var reader = new FileReader();
            reader.onload = function (evt) {
                console.log(evt);
                $('#selectedImg').attr('src', evt.target.result);
            };
            reader.onerror = function (evt) {
                console.error("An error ocurred reading the file", evt);
            };
            reader.readAsDataURL(file);

            var fileName = $('#keystoreFile').val();
            console.log(fileName)

            console.log(file)

            $("#selectedFile").text(file.name);

            console.log(reader)
            var filename = $('input[type=file]').val().split('\\').pop();
            console.log(filename);

            $('#fileName').text(filename);
        }
    }, false);


});


function checkBrowserIsSupportFileSelect() {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        // Read files
    } else {
        alert('The File APIs are not fully supported by your browser.');
    }
}

function initCrossAjax() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

}

function disconnectMetamask() {
    $("#connectBtnDiv").show();
    $("#walletAddressDiv").hide();
    window.location.href = '/';
}


async function getAccount() {
    return web3.eth.getAccounts();
}

async function checkAccountChange() {
    var account = await getAccount();
    console.log("checkAccountChange is started")
    setInterval(async () => {
        var tempAccount = await getAccount();
        if (tempAccount === undefined || tempAccount === null) {
            // if account changed to undefined, that means metamask is now locked
            disconnectMetamask()
        }
        if (tempAccount.toString().toUpperCase() !== account.toString().toUpperCase()) {
            account = await getAccount();
            await updateUI(account[0])
        }
    }, 1000);
}

async function updateUI(walletAddress) {
    if (walletAddress === undefined || walletAddress === null) {
        disconnectMetamask();
    }
    // set wallet address
    $("#connectBtnDiv").hide();
    $("#walletAddressDiv").show();
    $("#walletAddress").text(walletAddress);
    $("#myfilesUrl").attr("href", "/myfiles/" + walletAddress)
    console.log(walletAddress)
}

async function checkEthereumNetwork() {
    if (web3) {
        console.log("network id : " + await web3.eth.net.getNetworkType());
        switch (await web3.eth.net.getNetworkType()) {
            case 'main':
                console.log('This is mainnet');
                break;
            default:
                console.log('This is an unknown network.');
        }
        const desiredNetwork = 'ropsten';
        if (await web3.eth.net.getNetworkType() !== desiredNetwork) {
            // ask user to switch to desired network
            // alert('Please switch to ropsten network.');
        }
    }
}


upload_image = function (event) {
    if (selectedFile !== undefined) {
        var walletAddress = $('#walletAddress').text()
        var data = {
            'wallet_address': walletAddress,
        };
        var formData = new FormData();
        formData.append('file', selectedFile);
        const data_ = JSON.stringify(data);
        formData.append('data', data_);
        $.ajax({
            type: 'POST',
            cache: false,
            processData: false,
            contentType: false,
            url: '/api/v1/wallet/uploadImage/',
            data: formData,
            success: function (result) {
                console.log("Ssdff")
                if (result['status_code'] === 200) {
                    console.log(result['data'])
                    showNFTFiles(result['data'])
                } else {
                    var message = result['message'];
                    $('#errorMessage').text(message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    } else {
        console.log("Please select file")
    }
    return false
}


function showNFTFiles(nftFiles) {
    $("#nftContainer").empty();
    let txHash = nftFiles['txHash']
    let fullBase64 = nftFiles['fullBase64']
    $("#copyTarget").val(fullBase64);
    let tokenIds = nftFiles['tokenIds']
    let filePortions = nftFiles['filePortions']
    let testnetUrl = 'https://testnet.bscscan.com/tx/' + txHash;
    $("#txHashA").attr("href", testnetUrl)
    $("#txHashP").text(testnetUrl)

    var jjs = '<div class="Token_id">' +
        '<div class="tokken_name">' + 'Token ID : ' + 3 + '</div>\n' +
        +'<div class="tokken_hash_id">' + '<p>' + txHash + '</p>' + '</div>' +
        '</div>'
    for (var i = 0; i < tokenIds.length; i++) {
        var ht = '<div class="Token_id">' +
            '<div class="tokken_name">' + 'Token ID : ' + tokenIds[i] + '</div>\n' +
            '<div class="tokken_hash_id">' + '<p>' + filePortions[i] + '</p>' + '</div>' +
            '</div>'
        $("#nftContainer").append(ht);
    }
}

function copyBase64() {
    var clipboardText = "";
    clipboardText = $('#copyTarget').val();
    console.log(clipboardText);
    copyToClipboard(clipboardText);
    alert("Copied to Clipboard");
}

function copyToClipboard(text) {

    var textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copying text command was ' + msg);
    } catch (err) {
        console.log('Oops, unable to copy', err);
    }
    document.body.removeChild(textArea);
}