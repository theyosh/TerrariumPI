export const updateSiteBar = () => {
  const url = window.location.hash + (window.location.hash.slice(-1) !== '/' ? '/' : '');
  const sidebar = jQuery('ul.nav-sidebar');
  const menuitem = sidebar.find('a[href="' + url + '"]');

  // Reset sidebar
  sidebar.find('ul.nav.nav-treeview').hide();
  sidebar.find('*').removeClass('active menu-is-opening menu-open');

  // Activate menu and parent menu (if applicable)
  menuitem.toggleClass('active', true).parents('ul').show().parents('li').toggleClass('menu-is-opening menu-open', true).find('a:first').toggleClass('active', true);
};

export const toggleSidebarAdminActions = (isAdmin) => {
  const menuItems = document.querySelectorAll('div.sidebar nav.mt-2 ul.nav-sidebar .disabled' + (!isAdmin ? '-tmp' : ''));
  for (let menuItem of menuItems) {
    menuItem.classList.remove('disabled' + (!isAdmin ? '-tmp' : ''));
    menuItem.classList.add('disabled' + (isAdmin ? '-tmp' : ''));
  }
};