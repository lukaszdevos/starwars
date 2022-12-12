function addParams(header) {
    const searchParams = new URLSearchParams(window.location.search);
    let aggregations = searchParams.getAll('agg');
    if (!!aggregations.includes(header)) {
        aggregations = aggregations.filter(e => e !== header);
        if (!aggregations.length) {
            searchParams.delete("agg");
        } else {
            searchParams.delete("agg");
            aggregations.forEach(agg => searchParams.append("agg", agg))
        }
    } else {
        searchParams.append('agg', header);
    }
    window.location = window.location.pathname + '?' + searchParams.toString();
}