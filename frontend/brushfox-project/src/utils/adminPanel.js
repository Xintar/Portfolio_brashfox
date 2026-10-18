import { apiService } from '../services/api';
import { ADMIN_SSO_URL, ADMIN_URL } from './constants';

const ADMIN_WINDOW_NAME = 'foxbrush-admin';

/**
 * Open the Django admin already logged in as the current frontend user.
 * The window is opened synchronously (inside the click) so popup blockers allow it,
 * then a one-time ticket is POSTed to the backend, which starts the admin session.
 */
export const openAdminPanel = async () => {
  const adminWindow = window.open('', ADMIN_WINDOW_NAME);
  const target = adminWindow ? ADMIN_WINDOW_NAME : '_self';

  try {
    const { data } = await apiService.getAdminSsoTicket();

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = ADMIN_SSO_URL;
    form.target = target;

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'ticket';
    input.value = data.ticket;
    form.appendChild(input);

    document.body.appendChild(form);
    form.submit();
    form.remove();
  } catch (error) {
    // Fall back to the regular admin login page
    if (adminWindow) {
      adminWindow.location.href = ADMIN_URL;
    } else {
      window.location.href = ADMIN_URL;
    }
    throw error;
  }
};
