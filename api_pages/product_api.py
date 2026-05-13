"""
商品 API
"""

from .base_api import BaseAPI


class ProductAPI(BaseAPI):
    """商品接口封装"""

    def get_product_list(self, page: int = 1, size: int = 10):
        """获取商品列表"""
        return self.get("/index.php?s=/api/goods/index", params={
            "page": page,
            "size": size
        })

    def get_product_detail(self, goods_id: int):
        """获取商品详情"""
        return self.get("/index.php?s=/api/goods/detail", params={
            "id": goods_id
        })

    def search_product(self, keywords: str, page: int = 1, size: int = 10):
        """搜索商品"""
        return self.get("/index.php?s=/api/goods/search", params={
            "keywords": keywords,
            "page": page,
            "size": size
        })

    def get_category_list(self):
        """获取分类列表"""
        return self.get("/index.php?s=/api/goodscategory/index")