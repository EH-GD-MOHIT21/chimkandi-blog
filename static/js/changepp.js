function usercheck() {
    var changepp = document.getElementById("cpp").value;
    document.getElementById("ppupdateform").submit();
}
document.getElementById('cpp').addEventListener("change", function() {
    console.log('it works')
    usercheck()
})

document.getElementById('hojs').addEventListener('mouseover', function() {

})