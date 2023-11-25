function deleteProduct(productId) {
  let path = "delete_product/" + productId;
  let newPath = "/" + path;
  let currentPath = window.location.pathname;
  let filteredPath = currentPath.replace(/\/product_list\/\d+\//, newPath);
  window.location.href = filteredPath;
}

function editProduct(productId) {
  let path = "edit_product/" + productId;
  location.replace(path);
}