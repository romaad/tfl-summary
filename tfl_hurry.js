function getIdFromURL(){
    var url = window.location.href;
    // decde url query string
    var query = url.split('?')[1];
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == 'CardDisplayId') {
            return decodeURIComponent(pair[1]);
        }
    }
    alert('CardDisplayId not found in URL');
    return null;
}

function downloadUri(uri, filename) {
    var link = document.createElement('a');
    link.href = uri;
    link.download = filename;
    link.click();
}

function getBills(year /*number*/, startMonth = 1, endMonth = 12) {
    const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ];
    cardId = getIdFromURL();
    if (cardId == null) {
        return;
    }
    for (let month = startMonth ; month <= endMonth; month++) {
        monthName = monthNames[month-1];
        csvUri = `https://contactless.tfl.gov.uk/NewStatements/DownloadBillingCsv?CardDisplayId=${cardId}&Period=${month}%7C${year}`
        pdfUri = `https://contactless.tfl.gov.uk/NewStatements/Billing?Period=${month}%7C${year}&CardDisplayId=${cardId}&`
        downloadUri(csvUri, `${monthName}_${year}.csv`);
        // downloadUri(pdfUri, `${monthName}_${year}.pdf`);
    }
}
