//If Analytics is not enable, an error message will shown in console.
//You can change #error to #warning if you think #error is too hard.
#if !UNITY_ANALYTICS
#error "Analytics is not enabled!"
#endif

//Versions <5.5 don't have UnityEditor.Analytics
#if UNITY_EDITOR && UNITY_5_5_OR_NEWER
using UnityEngine;
using UnityEditor;
using UnityEditor.Analytics;
using UnityEditor.Callbacks;

public class AnalyticsCheck
{
    [PostProcessBuildAttribute(0)]
    public static void OnPostprocessBuild(BuildTarget target, string pathToBuiltProject)
    {
        //Check Analytics state when build is done.
        if (!AnalyticsSettings.enabled)
        {
            Debug.LogError("Analytics is not enabled!");
        }
    }
}
#endif
