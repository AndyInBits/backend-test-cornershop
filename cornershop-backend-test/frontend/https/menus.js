import axios from 'axios';

export default new (class MenuServices {

  menu_list(token) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/menus/`,
				method: 'GET'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					resolve(err);
				});
		});
	}

  menu_option_list(token) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/menu/options/`,
				method: 'GET'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					resolve(err);
				});
		});
	}

	menu_create(token, data) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/menus/`,
				method: 'POST',
				data
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err.response.data);
				});
		});
	}

  menu_delete(token, menuId) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/menus/${menuId}/`,
				method: 'DELETE'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err.response.data);
				});
		});
	}

  menu_detail(token, menuId) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/menus/${menuId}/`,
				method: 'GET'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err.response.data);
				});
		});
	}

	menu_edit(token, data) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/menus/${data.pk}/`,
				method: 'PUT',
				data
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err.response.data);
				});
		});
	}

	menu_option_create(token, data) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/menu/options/`,
				method: 'POST',
				data
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err.response.data);
				});
		});
	}
})();
