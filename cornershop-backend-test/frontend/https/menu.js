import axios from 'axios';

export default new (class MenuTodayServices {

  menu_today(uuid) {
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/today/menu/${uuid}`,
				method: 'GET'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err);
				});
		});
	}

	create_order(data) {
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/orders/`,
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
