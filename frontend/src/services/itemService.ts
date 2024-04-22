import MakeRequest from '@/services/apiRequest';

export const getItems = async () => {
  const endpoint = '/items';
  const method = 'GET';
  try {
    const items = await MakeRequest({ endpoint, method });
    return items;
  } catch (error) {
    console.log('Error getting items');
  }
};
