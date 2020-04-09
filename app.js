window.onload = function () {
    const submitButton = document.getElementById('submitButton');

    submitButton.addEventListener('click', () => {
        document.getElementById("is-problem").innerHTML = "Fetching...";
        document.getElementById("allocated-size").innerHTML = "Fetching...";
        document.getElementById("peak-size").innerHTML = "Fetching...";
        document.getElementById("problem").innerHTML = "Fetching...";
		document.getElementById("throughput").innerHTML = "Fetching...";

        const fileObject = document.getElementById('logger').files[0];
        if (fileObject) {
            return fetch("http://api.gceasy.io/analyzeGC?apiKey=384498af-3289-4474-bd6b-60ca270b4a1a", {
                method: 'POST',
                mode: 'cors',
                body: fileObject,
            })
                .then(response => response.json())
                .then(res => {
                    const {isProblem, problem, jvmHeapSize, throughputPercentage} = res;
                    const {allocatedSize, peakSize} = jvmHeapSize.total;
                    const problems = problem.map((it) => '<li>' + it + '</li>');

                    document.getElementById("is-problem").innerHTML = isProblem;
                    document.getElementById("allocated-size").innerHTML = allocatedSize;
                    document.getElementById("peak-size").innerHTML = peakSize;
                    document.getElementById("problem").innerHTML = problems.join("");
					document.getElementById("throughput").innerHTML = throughputPercentage;
                });
        }
    });
};
