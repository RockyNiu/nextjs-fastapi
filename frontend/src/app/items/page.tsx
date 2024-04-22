'use client';

import { getItems } from '@/services/itemService';
import { useEffect, useState } from 'react';
interface Item {
  id: number;
  name: string;
  date_created: string;
  date_updated: string;
}

const ItemPage = () => {
  const [items, setItems] = useState<Item[]>([]);
  useEffect(() => {
    getItems().then((items) => {
      setItems(items);
      console.log(items);
    });
  }, []);

  return (
    <div className="flex-y justify-content-center space-y-4 m-4">
      <div className="">
        <h1>Item Page</h1>
      </div>
      <div>
        <table className="table table-striped border-spacing-1 border">
          <thead>
            <tr>
              <th className="border border-gray-400 px-4 py-2">Name</th>
              <th className="border border-gray-400 px-4 py-2">Date Created</th>
              <th className="border border-gray-400 px-4 py-2">Date Updated</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td className="border border-gray-400 px-4 py-2er">
                  {item.name}
                </td>
                <td className="border border-gray-400 px-4 py-2">
                  {item.date_created}
                </td>
                <td className="border border-gray-400 px-4 py-2">
                  {item.date_updated}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ItemPage;
