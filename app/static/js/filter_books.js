function toggleFavouriteFilter() {
    const currentUrl = new URL(window.location.href);
    const isFavourites = currentUrl.searchParams.get("favourites") === "1";
    const newFavourites = isFavourites ? "0" : "1";

    const viewMode = document.querySelector(".btn-group .active").getAttribute("href").includes("view=row") ? "row" : "card";
    currentUrl.searchParams.set("favourites", newFavourites);
    currentUrl.searchParams.set("view", viewMode);

    window.location.href = currentUrl.toString();
}