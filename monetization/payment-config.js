// 支付配置文件
// 在此配置你的收款信息

const PAYMENT_CONFIG = {
  // 产品价格配置 (单位: 元)
  products: {
    'efficiency-toolkit': {
      name: '效率工具包 v2.0',
      price: 29,
      originalPrice: 99,
      discount: '限时特价',
      description: '7个实用工具 + 3个自动化脚本'
    },
    'automation-scripts': {
      name: '自动化脚本包',
      price: 19,
      originalPrice: 59,
      discount: '新用户专享',
      description: '5个Python自动化脚本'
    },
    'personal-brand': {
      name: '个人品牌打造手册',
      price: 39,
      originalPrice: 129,
      discount: '早鸟价',
      description: '30天系统打造个人品牌'
    },
    'copywriting-library': {
      name: '朋友圈文案库',
      price: 9.9,
      originalPrice: 29,
      discount: '限时优惠',
      description: '1000+高质量文案模板'
    }
  },

  // 支付方式配置
  paymentMethods: {
    wechat: {
      enabled: true,
      qrcode: 'https://你的微信收款码图片URL.jpg',  // 替换为你的微信收款码图片链接
      name: '微信支付'
    },
    alipay: {
      enabled: true,
      qrcode: 'https://你的支付宝收款码图片URL.jpg',  // 替换为你的支付宝收款码图片链接
      name: '支付宝'
    }
  },

  // 联系方式
  contact: {
    wechat: '你的微信号',  // 替换为你的微信号
    phone: '18291161026',
    email: 'your-email@example.com'
  },

  // 收款后自动发货配置 (可选)
  autoDelivery: {
    enabled: false,
    // 如果使用第三方支付平台，可以在这里配置回调地址
    webhookUrl: ''
  }
};

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PAYMENT_CONFIG;
}
