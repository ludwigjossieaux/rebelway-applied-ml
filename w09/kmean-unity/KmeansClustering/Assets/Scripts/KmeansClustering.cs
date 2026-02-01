using UnityEngine;
using System.Linq;
using System.Collections.Generic;
using System;
using System.Collections;

public class KmeansClustering : MonoBehaviour
{
    public int numberOfSpheres = 100;
    public int numberOfClusters = 3;
    public GameObject spherePrefab;
    public Vector3 spaceSize = new Vector3(10, 10, 10);

    private List<GameObject> spheres = new List<GameObject>();
    private Vector3[] centroids;
    private Dictionary<int, List<GameObject>> clusters = new Dictionary<int, List<GameObject>>();

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        GenerateSpheres();
        InitializeCentroids();
        StartCoroutine(ClusterSpheres());
    }

    private IEnumerator ClusterSpheres()
    {
        bool centroidChanged = true;

        while(centroidChanged)
        {
            clusters.Clear();
            for(int i = 0; i < numberOfClusters; i++)
            {
                clusters[i] = new List<GameObject>();
            }
            foreach(var sphere in spheres)
            {
                float minDistance = float.MaxValue;
                int closestCentroid = 0;
                for(int i = 0; i < centroids.Length; i++)
                {
                    float distance = Vector3.Distance(sphere.transform.position, centroids[i]);
                    if(distance < minDistance)
                    {
                        minDistance = distance;
                        closestCentroid = i;
                    }
                }
                clusters[closestCentroid].Add(sphere);
            }

            centroidChanged = UpdateCentroids();
            VisualizeClusters();

            //yield return null;
            yield return new WaitForSeconds(1f);
        }
    }

    private bool UpdateCentroids()
    {
        bool changed = false;
        for (int i = 0; i < numberOfClusters; i++)
        {
            if(clusters[i].Count == 0) continue;
            Vector3 newCentroid = Vector3.zero;
            foreach(var sphere in clusters[i])
            {
                newCentroid += sphere.transform.position;
            }
            newCentroid /= clusters[i].Count;
            if(newCentroid != centroids[i])
            {
                centroids[i] = newCentroid;
                changed = true;
            }
        }
        return changed;
    }

    private void VisualizeClusters()
    {
        Color[] colors = { Color.red, Color.green, Color.blue, Color.yellow, Color.cyan, Color.magenta };
        for(int i = 0; i < numberOfClusters; i++)
        {
            Color clusterColor = colors[i % colors.Length];
            foreach(var sphere in clusters[i])
            {
                sphere.GetComponent<Renderer>().material.color = clusterColor;
            }
        }
    }

    private void InitializeCentroids()
    {
        centroids = new Vector3[numberOfClusters];
        for(int i = 0; i < numberOfClusters; i++)
        {
            centroids[i] = spheres[UnityEngine.Random.Range(0, spheres.Count)].transform.position;
        }
    }

    private void GenerateSpheres()
    {
        for(int i = 0; i < numberOfSpheres; i++)
        {
            Vector3 position = new Vector3(
                UnityEngine.Random.Range(-spaceSize.x / 2, spaceSize.x / 2),
                UnityEngine.Random.Range(-spaceSize.y / 2, spaceSize.y / 2),
                UnityEngine.Random.Range(-spaceSize.z / 2, spaceSize.z / 2)
            );
            GameObject sphere = Instantiate(spherePrefab, position, Quaternion.identity);
            spheres.Add(sphere);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
