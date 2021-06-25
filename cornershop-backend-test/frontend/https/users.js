import axios from 'axios';

export default new (class UsersServices {
	user_list(token) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/users/`,
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

	user_create(token, data) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/users/`,
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

	user_detail(token, userId) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/users/${userId}/`,
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

	user_edit(token, data) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/users/${data.pk}/`,
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
	user_delete(token, userId) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/users/${userId}/`,
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


})();
