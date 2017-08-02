//If Analytics is not enable, an error message will shown in console.
//You can change #error to #warning if you think #error is too hard.
#if !UNITY_ANALYTICS
#error "Analytics is not enabled!"
#endif