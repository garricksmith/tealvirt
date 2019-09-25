<script>
    function doPost(param){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "index.py", false);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(param);
        document.getElementById("page-content").innerHTML = xhttp.responseText;
    }
    function startVM(vm){
        var vmStatus = document.getElementById("vm-status-"+vm);
        alert("Starting VM...");
        vmStatus.innerHTML = "Running";
    }
    function stopVM(vm){
        var vmStatus = document.getElementById("vm-status-"+vm);
        alert("Stopping VM...");
        vmStatus.innerHTML = "Stopped";
    }
</script>
