document.addEventListener('DOMContentLoaded', () => {
    const headerHTML = `
    <header>
        <ul>
            <li>
                <button class="bi bi-pencil-square" id="GotoEdit" aria-label="Edit"></button>
            </li> 
            <li>
                <button class="bi bi-house-door-fill" id="GotoHome" aria-label="Home"></button>
            </li>
            <li>
               <button class="bi bi-search" id="Search" aria-label="Search"></button>
            </li>
        </ul>
    </header>
    `;

    document.getElementById("header").innerHTML = headerHTML;
    const EditButton=document.getElementById("GotoEdit");
    const HomeButton=document.getElementById("GotoHome");
    const SearchButton=document.getElementById("Search");
    EditButton.addEventListener("click",async function (event){
        event.preventDefault();
        window.location.href="luckypocket.html";

    })
    HomeButton.addEventListener("click",async function (event){
        event.preventDefault();
        window.location.href="main.html";
    })
    SearchButton.addEventListener("click",async function (event){
        event.preventDefault();
        window.location.href="search.html";
    })


});
