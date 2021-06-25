import axios from 'axios';

export default new (class AuthServices {
	login(email, password) {
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/login`,
				method: 'POST',
				data: {
					email,
					password,
				},
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					resolve(err);
				});
		});
	}

  getMe(token) {
		return new Promise(resolve => {
      axios.defaults.headers.common[
				'Authorization'
			] = `Bearer ${token}`;
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/get/me`,
				method: 'GET'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					return err;
				});
		});
	}

})();
